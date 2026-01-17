package org.gua.gua.ui.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import org.gua.gua.data.local.UserPreferences
import org.gua.gua.data.model.User
import org.gua.gua.utils.ValidationUtils
import javax.inject.Inject

@HiltViewModel
class LoginViewModel @Inject constructor(
    private val userPreferences: UserPreferences
) : ViewModel() {
    
    private val _usernameError = MutableLiveData<String?>()
    val usernameError: LiveData<String?> = _usernameError
    
    private val _emailError = MutableLiveData<String?>()
    val emailError: LiveData<String?> = _emailError
    
    private val _loginError = MutableLiveData<String?>()
    val loginError: LiveData<String?> = _loginError
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _loginSuccess = MutableLiveData<Boolean>()
    val loginSuccess: LiveData<Boolean> = _loginSuccess
    
    fun validateUsername(username: String) {
        _usernameError.value = ValidationUtils.validateUsername(username)
    }
    
    fun validateEmail(email: String) {
        _emailError.value = ValidationUtils.validateEmail(email)
    }
    
    fun login(username: String, email: String) {
        // Clear previous errors
        _loginError.value = null
        
        // Validate inputs
        val usernameError = ValidationUtils.validateUsername(username)
        val emailError = ValidationUtils.validateEmail(email)
        
        _usernameError.value = usernameError
        _emailError.value = emailError
        
        if (usernameError != null || emailError != null) {
            _loginError.value = "Please fix the errors above"
            return
        }
        
        // Simulate login process
        viewModelScope.launch {
            _isLoading.value = true
            
            // Simulate network delay
            delay(1500)
            
            try {
                // Save user data
                val user = User(
                    username = username,
                    email = email,
                    disclaimerAccepted = userPreferences.isDisclaimerAccepted()
                )
                userPreferences.saveUser(user)
                
                _loginSuccess.value = true
            } catch (e: Exception) {
                _loginError.value = "Login failed. Please try again."
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    fun loginAsGuest() {
        viewModelScope.launch {
            _isLoading.value = true
            
            // Simulate delay
            delay(1000)
            
            try {
                // Save guest user
                val guestUser = User(
                    username = "Guest",
                    email = "guest@gua.app",
                    disclaimerAccepted = userPreferences.isDisclaimerAccepted()
                )
                userPreferences.saveUser(guestUser)
                
                _loginSuccess.value = true
            } catch (e: Exception) {
                _loginError.value = "Failed to continue as guest. Please try again."
            } finally {
                _isLoading.value = false
            }
        }
    }
}