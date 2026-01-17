package org.gua.gua.ui.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import org.gua.gua.data.local.UserPreferences
import org.gua.gua.data.repository.GameRepository
import javax.inject.Inject

@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val userPreferences: UserPreferences,
    private val gameRepository: GameRepository
) : ViewModel() {
    
    private val _cacheSize = MutableLiveData<String>()
    val cacheSize: LiveData<String> = _cacheSize
    
    private val _historyCount = MutableLiveData<Int>()
    val historyCount: LiveData<Int> = _historyCount
    
    private val _currentTheme = MutableLiveData<String>()
    val currentTheme: LiveData<String> = _currentTheme
    
    init {
        loadSettings()
    }
    
    private fun loadSettings() {
        viewModelScope.launch {
            try {
                _cacheSize.value = calculateCacheSize()
                _historyCount.value = gameRepository.getHistoryCount()
                _currentTheme.value = userPreferences.getTheme()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
    
    fun toggleTheme() {
        viewModelScope.launch {
            val currentTheme = userPreferences.getTheme()
            val newTheme = if (currentTheme == "Dark") "Light" else "Dark"
            userPreferences.setTheme(newTheme)
            _currentTheme.value = newTheme
        }
    }
    
    fun clearCache() {
        viewModelScope.launch {
            try {
                gameRepository.clearCache()
                _cacheSize.value = "0 MB"
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
    
    fun clearExpiredCache() {
        viewModelScope.launch {
            try {
                gameRepository.clearExpiredCache()
                _cacheSize.value = calculateCacheSize()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
    
    fun clearHistory() {
        viewModelScope.launch {
            try {
                gameRepository.clearHistory()
                _historyCount.value = 0
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
    
    private suspend fun calculateCacheSize(): String {
        return try {
            val sizeInMB = gameRepository.getCacheSize() / (1024 * 1024)
            "$sizeInMB MB"
        } catch (e: Exception) {
            "Unknown"
        }
    }
}