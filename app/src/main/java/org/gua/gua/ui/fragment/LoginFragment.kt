package org.gua.gua.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.animation.AnimationUtils
import androidx.core.widget.doOnTextChanged
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.fragment.app.viewModels
import com.google.android.material.snackbar.Snackbar
import dagger.hilt.android.AndroidEntryPoint
import org.gua.gua.R
import org.gua.gua.databinding.FragmentLoginBinding
import org.gua.gua.ui.viewmodel.LoginViewModel
import org.gua.gua.ui.viewmodel.MainViewModel

@AndroidEntryPoint
class LoginFragment : Fragment() {
    
    private var _binding: FragmentLoginBinding? = null
    private val binding get() = _binding!!
    
    private val viewModel: LoginViewModel by viewModels()
    private val mainViewModel: MainViewModel by activityViewModels()
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentLoginBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        setupUI()
        observeViewModel()
    }
    
    private fun setupUI() {
        // Real-time validation
        binding.usernameEditText.doOnTextChanged { text, _, _, _ ->
            viewModel.validateUsername(text.toString())
        }
        
        binding.emailEditText.doOnTextChanged { text, _, _, _ ->
            viewModel.validateEmail(text.toString())
        }
        
        // Login button
        binding.loginButton.setOnClickListener {
            val username = binding.usernameEditText.text.toString()
            val email = binding.emailEditText.text.toString()
            viewModel.login(username, email)
        }
        
        // Guest button
        binding.guestButton.setOnClickListener {
            viewModel.loginAsGuest()
        }
    }
    
    private fun observeViewModel() {
        viewModel.usernameError.observe(viewLifecycleOwner) { error ->
            binding.usernameLayout.error = error
            if (error != null) {
                shakeView(binding.usernameLayout)
            }
        }
        
        viewModel.emailError.observe(viewLifecycleOwner) { error ->
            binding.emailLayout.error = error
            if (error != null) {
                shakeView(binding.emailLayout)
            }
        }
        
        viewModel.loginError.observe(viewLifecycleOwner) { error ->
            if (error != null) {
                binding.errorText.text = error
                binding.errorText.visibility = android.view.View.VISIBLE
                shakeView(binding.loginCard)
            } else {
                binding.errorText.visibility = android.view.View.GONE
            }
        }
        
        viewModel.isLoading.observe(viewLifecycleOwner) { isLoading ->
            binding.loginButton.isEnabled = !isLoading
            binding.guestButton.isEnabled = !isLoading
            binding.progressBar.visibility = if (isLoading) android.view.View.VISIBLE else android.view.View.GONE
        }
        
        viewModel.loginSuccess.observe(viewLifecycleOwner) { success ->
            if (success) {
                Snackbar.make(binding.root, "Login successful!", Snackbar.LENGTH_SHORT).show()
                mainViewModel.onUserLoggedIn()
            }
        }
    }
    
    private fun shakeView(view: View) {
        val shake = AnimationUtils.loadAnimation(requireContext(), R.anim.shake)
        view.startAnimation(shake)
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}