package org.gua.gua.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.android.material.snackbar.Snackbar
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
        
        setupRecyclerView()
        observeViewModel()
        
        // Load games
        viewModel.loadLatestGames()
    }
    
    private fun setupRecyclerView() {
        gameAdapter = GameAdapter { game ->
            // Navigate to game details - simplified navigation
            // TODO: Implement proper navigation to game details
            // For now, just show a toast or log
            android.util.Log.d("HomeFragment", "Game clicked: ${game.name}")
        }
        
        binding.gamesRecyclerView.apply {
            layoutManager = LinearLayoutManager(requireContext())
            adapter = gameAdapter
        }
        
        // Swipe to refresh
        binding.swipeRefreshLayout.setOnRefreshListener {
            viewModel.refreshGames()
        }
    }
    
    private fun observeViewModel() {
        viewModel.games.observe(viewLifecycleOwner) { games ->
            gameAdapter.submitList(games)
        }
        
        viewModel.isLoading.observe(viewLifecycleOwner) { isLoading ->
            binding.swipeRefreshLayout.isRefreshing = isLoading
            binding.progressBar.visibility = if (isLoading && gameAdapter.itemCount == 0) {
                android.view.View.VISIBLE
            } else {
                android.view.View.GONE
            }
        }
        
        viewModel.error.observe(viewLifecycleOwner) { error ->
            if (error != null) {
                Snackbar.make(binding.root, error, Snackbar.LENGTH_LONG)
                    .setAction("Retry") {
                        viewModel.loadLatestGames()
                    }
                    .show()
            }
        }
        
        viewModel.isEmpty.observe(viewLifecycleOwner) { isEmpty ->
            binding.emptyView.visibility = if (isEmpty) android.view.View.VISIBLE else android.view.View.GONE
            binding.gamesRecyclerView.visibility = if (isEmpty) android.view.View.GONE else android.view.View.VISIBLE
        }
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}