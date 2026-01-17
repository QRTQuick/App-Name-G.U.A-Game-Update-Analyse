package org.gua.gua.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.navArgs
import com.bumptech.glide.Glide
import dagger.hilt.android.AndroidEntryPoint
import org.gua.gua.databinding.FragmentGameDetailsBinding
import org.gua.gua.ui.viewmodel.GameDetailsViewModel

@AndroidEntryPoint
class GameDetailsFragment : Fragment() {
    
    private var _binding: FragmentGameDetailsBinding? = null
    private val binding get() = _binding!!
    
    private val args: GameDetailsFragmentArgs by navArgs()
    private val viewModel: GameDetailsViewModel by viewModels()
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentGameDetailsBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        setupClickListeners()
        observeViewModel()
        
        viewModel.loadGameDetails(args.gameId)
    }
    
    private fun setupClickListeners() {
        binding.favoriteButton.setOnClickListener {
            viewModel.toggleFavorite()
        }
        
        binding.backButton.setOnClickListener {
            requireActivity().onBackPressed()
        }
    }
    
    private fun observeViewModel() {
        viewModel.gameDetails.observe(viewLifecycleOwner) { game ->
            game?.let {
                binding.gameTitle.text = it.name
                binding.gameDescription.text = it.description
                binding.ratingText.text = it.rating.toString()
                binding.releasedText.text = it.released
                binding.platformsText.text = it.platforms.joinToString(", ")
                binding.genresText.text = it.genres.joinToString(", ")
                binding.developersText.text = it.developers.joinToString(", ")
                binding.publishersText.text = it.publishers.joinToString(", ")
                
                Glide.with(this)
                    .load(it.backgroundImage)
                    .into(binding.gameImage)
            }
        }
        
        viewModel.isFavorite.observe(viewLifecycleOwner) { isFavorite ->
            binding.favoriteButton.text = if (isFavorite) {
                "Remove from Favorites"
            } else {
                "Add to Favorites"
            }
        }
        
        viewModel.isLoading.observe(viewLifecycleOwner) { isLoading ->
            binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
            binding.contentScrollView.visibility = if (isLoading) View.GONE else View.VISIBLE
        }
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}