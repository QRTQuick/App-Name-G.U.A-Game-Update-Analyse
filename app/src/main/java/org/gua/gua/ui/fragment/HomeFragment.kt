package org.gua.gua.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.LinearLayoutManager
import dagger.hilt.android.AndroidEntryPoint
import org.gua.gua.databinding.FragmentHomeBinding
import org.gua.gua.ui.adapter.GameAdapter
import org.gua.gua.ui.viewmodel.HomeViewModel

@AndroidEntryPoint
class HomeFragment : Fragment() {
    
    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!
    
    private val viewModel: HomeViewModel by viewModels()
    private lateinit var gameAdapter: GameAdapter
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        try {
            setupRecyclerView()
            observeViewModel()
            
            // Load games
            viewModel.loadLatestGames()
        } catch (e: Exception) {
            e.printStackTrace()
            // Show error state
            binding.emptyView.visibility = View.VISIBLE
            binding.gamesRecyclerView.visibility = View.GONE
        }
    }
    
    private fun setupRecyclerView() {
        gameAdapter = GameAdapter { game ->
            // Simple click handling - just log for now
            android.util.Log.d("HomeFragment", "Game clicked: ${game.name}")
        }
        
        binding.gamesRecyclerView.apply {
            layoutManager = LinearLayoutManager(requireContext())
            adapter = gameAdapter
        }
        
        // Swipe to refresh
        binding.swipeRefreshLayout.setOnRefreshListener {
            try {
                viewModel.refreshGames()
            } catch (e: Exception) {
                e.printStackTrace()
                binding.swipeRefreshLayout.isRefreshing = false
            }
        }
    }
    
    private fun observeViewModel() {
        try {
            viewModel.games.observe(viewLifecycleOwner) { games ->
                if (games != null) {
                    gameAdapter.submitList(games)
                }
            }
            
            viewModel.isLoading.observe(viewLifecycleOwner) { isLoading ->
                binding.swipeRefreshLayout.isRefreshing = isLoading ?: false
                binding.progressBar.visibility = if (isLoading == true && gameAdapter.itemCount == 0) {
                    View.VISIBLE
                } else {
                    View.GONE
                }
            }
            
            viewModel.error.observe(viewLifecycleOwner) { error ->
                if (error != null) {
                    // Simple error handling - just log for now
                    android.util.Log.e("HomeFragment", "Error: $error")
                    binding.emptyView.visibility = View.VISIBLE
                }
            }
            
            viewModel.isEmpty.observe(viewLifecycleOwner) { isEmpty ->
                binding.emptyView.visibility = if (isEmpty == true) View.VISIBLE else View.GONE
                binding.gamesRecyclerView.visibility = if (isEmpty == true) View.GONE else View.VISIBLE
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}