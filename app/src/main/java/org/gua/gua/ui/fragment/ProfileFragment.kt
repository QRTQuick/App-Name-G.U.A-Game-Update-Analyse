package org.gua.gua.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.LinearLayoutManager
import dagger.hilt.android.AndroidEntryPoint
import org.gua.gua.databinding.FragmentProfileBinding
import org.gua.gua.ui.adapter.GameAdapter
import org.gua.gua.ui.viewmodel.ProfileViewModel

@AndroidEntryPoint
class ProfileFragment : Fragment() {
    
    private var _binding: FragmentProfileBinding? = null
    private val binding get() = _binding!!
    
    private val viewModel: ProfileViewModel by viewModels()
    private lateinit var recentGamesAdapter: GameAdapter
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentProfileBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        setupRecyclerView()
        setupClickListeners()
        observeViewModel()
        
        viewModel.loadUserProfile()
    }
    
    private fun setupRecyclerView() {
        recentGamesAdapter = GameAdapter { game ->
            android.util.Log.d("ProfileFragment", "Recent game clicked: ${game.name}")
        }
        
        binding.recentGamesRecyclerView.apply {
            layoutManager = LinearLayoutManager(requireContext(), LinearLayoutManager.HORIZONTAL, false)
            adapter = recentGamesAdapter
        }
    }
    
    private fun setupClickListeners() {
        binding.editProfileButton.setOnClickListener {
            // Navigate to edit profile
            android.util.Log.d("ProfileFragment", "Edit profile clicked")
        }
        
        binding.favoritesCard.setOnClickListener {
            // Navigate to favorites
            android.util.Log.d("ProfileFragment", "Favorites clicked")
        }
        
        binding.historyCard.setOnClickListener {
            // Navigate to history
            android.util.Log.d("ProfileFragment", "History clicked")
        }
        
        binding.notificationsCard.setOnClickListener {
            // Navigate to notifications
            android.util.Log.d("ProfileFragment", "Notifications clicked")
        }
        
        binding.logoutButton.setOnClickListener {
            viewModel.logout()
        }
    }
    
    private fun observeViewModel() {
        viewModel.userProfile.observe(viewLifecycleOwner) { user ->
            user?.let {
                binding.usernameText.text = it.username
                binding.emailText.text = it.email
            }
        }
        
        viewModel.userStats.observe(viewLifecycleOwner) { stats ->
            stats?.let {
                binding.gamesViewedText.text = it.gamesViewed.toString()
                binding.favoritesCountText.text = it.favoritesCount.toString()
                binding.reviewsCountText.text = it.reviewsCount.toString()
            }
        }
        
        viewModel.recentGames.observe(viewLifecycleOwner) { games ->
            recentGamesAdapter.submitList(games)
        }
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}