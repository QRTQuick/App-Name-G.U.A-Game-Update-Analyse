package org.gua.gua.ui.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import org.gua.gua.data.model.Game
import org.gua.gua.data.repository.GameRepository
import org.gua.gua.utils.Resource
import javax.inject.Inject

@HiltViewModel
class GameDetailsViewModel @Inject constructor(
    private val gameRepository: GameRepository
) : ViewModel() {
    
    private val _gameDetails = MutableLiveData<Game?>()
    val gameDetails: LiveData<Game?> = _gameDetails
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error
    
    private val _isFavorite = MutableLiveData<Boolean>()
    val isFavorite: LiveData<Boolean> = _isFavorite
    
    private var currentGameId: Int = 0
    
    fun loadGameDetails(gameId: Int) {
        currentGameId = gameId
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            try {
                when (val result = gameRepository.getGameDetails(gameId)) {
                    is Resource.Success -> {
                        _gameDetails.value = result.data
                        checkIfFavorite(gameId)
                        // Add to history
                        result.data?.let { gameRepository.addToHistory(it) }
                    }
                    is Resource.Error -> {
                        _error.value = result.message
                    }
                    is Resource.Loading -> {
                        // Already handled above
                    }
                }
            } catch (e: Exception) {
                _error.value = e.message
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    fun toggleFavorite() {
        viewModelScope.launch {
            try {
                val currentGame = _gameDetails.value
                if (currentGame != null) {
                    val isCurrentlyFavorite = _isFavorite.value ?: false
                    if (isCurrentlyFavorite) {
                        gameRepository.removeFavorite(currentGameId)
                        _isFavorite.value = false
                    } else {
                        gameRepository.addFavorite(currentGame)
                        _isFavorite.value = true
                    }
                }
            } catch (e: Exception) {
                _error.value = e.message
            }
        }
    }
    
    private suspend fun checkIfFavorite(gameId: Int) {
        try {
            _isFavorite.value = gameRepository.isFavorite(gameId)
        } catch (e: Exception) {
            _isFavorite.value = false
        }
    }
}