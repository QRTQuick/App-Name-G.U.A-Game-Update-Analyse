package org.gua.gua.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.LinearLayoutManager
import dagger.hilt.android.AndroidEntryPoint
import org.gua.gua.databinding.FragmentTrendingBinding
import org.gua.gua.ui.adapter.GameAdapter
import org.gua.gua.ui.viewmodel.TrendingViewModel

@AndroidEntryPoint
class TrendingFragment : Fragment() {
    
    private var _binding: FragmentTrendingBinding? = null
    private val binding get() = _binding!!
    
    private val viewModel: TrendingViewModel by viewModels()
    private lateinit var gameAdapter: GameAdapter
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentTrendingBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        setupRecyclerView()
        observeViewModel()
        
        // Load trending games
        viewModel.loadTrendingGames()
    }
    
    private fun setupRecyclerView() {
        gameAdapter = GameAdapter { game ->
            android.util.Log.d("TrendingFragment", "Game clicked: ${game.name}")
        }
        
        binding.trendingRecyclerView.apply {
            layoutManager = LinearLayoutManager(requireContext())
            adapter = gameAdapter
        }
        
        binding.swipeRefreshLayout.setOnRefreshListener {
            viewModel.refreshTrendingGames()
        }
    }
    
    private fun observeViewModel() {
        viewModel.trendingGames.observe(viewLifecycleOwner) { games ->
            gameAdapter.submitList(games)
        }
        
        viewModel.isLoading.observe(viewLifecycleOwner) { isLoading ->
            binding.swipeRefreshLayout.isRefreshing = isLoading
            binding.progressBar.visibility = if (isLoading && gameAdapter.itemCount == 0) {
                View.VISIBLE
            } else {
                View.GONE
            }
        }
        
        viewModel.isEmpty.observe(viewLifecycleOwner) { isEmpty ->
            binding.emptyView.visibility = if (isEmpty) View.VISIBLE else View.GONE
        }
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}