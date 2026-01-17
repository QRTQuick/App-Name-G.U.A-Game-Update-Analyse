package org.gua.gua.ui.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import dagger.hilt.android.lifecycle.HiltViewModel
import org.gua.gua.data.local.UserPreferences
import javax.inject.Inject

@HiltViewModel
class MainViewModel @Inject constructor(
    private val userPreferences: UserPreferences
) : ViewModel() {
    
    private val _navigationEvent = MutableLiveData<String>()
    val navigationEvent: LiveData<String> = _navigationEvent
    
    private val _showBottomNav = MutableLiveData<Boolean>()
    val showBottomNav: LiveData<Boolean> = _showBottomNav
    
    fun checkUserState() {
        when {
            !userPreferences.isDisclaimerAccepted() -> {
                _navigationEvent.value = "disclaimer"
                _showBottomNav.value = false
            }
            !userPreferences.isLoggedIn() -> {
                _navigationEvent.value = "login"
                _showBottomNav.value = false
            }
            else -> {
                _navigationEvent.value = "home"
                _showBottomNav.value = true
            }
        }
    }
    
    fun onDisclaimerAccepted() {
        userPreferences.acceptDisclaimer()
        if (userPreferences.isLoggedIn()) {
            _navigationEvent.value = "home"
            _showBottomNav.value = true
        } else {
            _navigationEvent.value = "login"
            _showBottomNav.value = false
        }
    }
    
    fun onUserLoggedIn() {
        _navigationEvent.value = "home"
        _showBottomNav.value = true
    }
    
    fun onUserLoggedOut() {
        userPreferences.logout()
        _navigationEvent.value = "login"
        _showBottomNav.value = false
    }
}