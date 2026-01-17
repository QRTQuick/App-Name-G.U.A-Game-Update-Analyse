package org.gua.gua.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import dagger.hilt.android.AndroidEntryPoint
import org.gua.gua.databinding.FragmentSettingsBinding
import org.gua.gua.ui.viewmodel.SettingsViewModel

@AndroidEntryPoint
class SettingsFragment : Fragment() {
    
    private var _binding: FragmentSettingsBinding? = null
    private val binding get() = _binding!!
    
    private val viewModel: SettingsViewModel by viewModels()
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentSettingsBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        setupClickListeners()
        observeViewModel()
    }
    
    private fun setupClickListeners() {
        binding.themeCard.setOnClickListener {
            viewModel.toggleTheme()
        }
        
        binding.languageCard.setOnClickListener {
            // Show language selection dialog
            android.util.Log.d("SettingsFragment", "Language selection clicked")
        }
        
        binding.clearCacheCard.setOnClickListener {
            viewModel.clearCache()
        }
        
        binding.clearExpiredCacheCard.setOnClickListener {
            viewModel.clearExpiredCache()
        }
        
        binding.clearHistoryCard.setOnClickListener {
            viewModel.clearHistory()
        }
        
        binding.aboutCard.setOnClickListener {
            // Show about dialog
            android.util.Log.d("SettingsFragment", "About clicked")
        }
        
        binding.privacyPolicyCard.setOnClickListener {
            // Open privacy policy
            android.util.Log.d("SettingsFragment", "Privacy policy clicked")
        }
        
        binding.termsCard.setOnClickListener {
            // Open terms of service
            android.util.Log.d("SettingsFragment", "Terms of service clicked")
        }
    }
    
    private fun observeViewModel() {
        viewModel.cacheSize.observe(viewLifecycleOwner) { size ->
            binding.cacheSizeText.text = size
        }
        
        viewModel.historyCount.observe(viewLifecycleOwner) { count ->
            binding.historyCountText.text = "$count items"
        }
        
        viewModel.currentTheme.observe(viewLifecycleOwner) { theme ->
            binding.themeValueText.text = theme
        }
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}