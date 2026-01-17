package org.gua.gua.ui.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import org.gua.gua.data.model.Game
import org.gua.gua.data.repository.GameRepository
import javax.inject.Inject

@HiltViewModel
class HistoryViewModel @Inject constructor(
    private val gameRepository: GameRepository
) : ViewModel() {
    
    private val _historyGames = MutableLiveData<List<Game>>()
    val historyGames: LiveData<List<Game>> = _historyGames
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error
    
    private val _isEmpty = MutableLiveData<Boolean>()
    val isEmpty: LiveData<Boolean> = _isEmpty
    
    fun loadHistory() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            try {
                val history = gameRepository.getGameHistory()
                _historyGames.value = history
                _isEmpty.value = history.isEmpty()
            } catch (e: Exception) {
                _error.value = e.message
                _isEmpty.value = true
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    fun clearHistory() {
        viewModelScope.launch {
            try {
                gameRepository.clearHistory()
                _historyGames.value = emptyList()
                _isEmpty.value = true
            } catch (e: Exception) {
                _error.value = e.message
            }
        }
    }
}