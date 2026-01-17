package org.gua.gua.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.GridLayoutManager
import dagger.hilt.android.AndroidEntryPoint
import org.gua.gua.databinding.FragmentFavoritesBinding
import org.gua.gua.ui.adapter.GameAdapter
import org.gua.gua.ui.viewmodel.FavoritesViewModel

@AndroidEntryPoint
class FavoritesFragment : Fragment() {
    
    private var _binding: FragmentFavoritesBinding? = null
    private val binding get() = _binding!!
    
    private val viewModel: FavoritesViewModel by viewModels()
    private lateinit var gameAdapter: GameAdapter
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentFavoritesBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        setupRecyclerView()
        observeViewModel()
        
        viewModel.loadFavoriteGames()
    }
    
    private fun setupRecyclerView() {
        gameAdapter = GameAdapter { game ->
            android.util.Log.d("FavoritesFragment", "Favorite game clicked: ${game.name}")
        }
        
        binding.favoritesRecyclerView.apply {
            layoutManager = GridLayoutManager(requireContext(), 2)
            adapter = gameAdapter
        }
        
        binding.swipeRefreshLayout.setOnRefreshListener {
            viewModel.refreshFavorites()
        }
    }
    
    private fun observeViewModel() {
        viewModel.favoriteGames.observe(viewLifecycleOwner) { games ->
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
            binding.favoritesRecyclerView.visibility = if (isEmpty) View.GONE else View.VISIBLE
        }
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}