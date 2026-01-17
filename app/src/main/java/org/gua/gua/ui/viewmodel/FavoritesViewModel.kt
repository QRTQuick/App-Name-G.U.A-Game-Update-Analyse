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
class FavoritesViewModel @Inject constructor(
    private val gameRepository: GameRepository
) : ViewModel() {
    
    private val _favoriteGames = MutableLiveData<List<Game>>()
    val favoriteGames: LiveData<List<Game>> = _favoriteGames
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error
    
    private val _isEmpty = MutableLiveData<Boolean>()
    val isEmpty: LiveData<Boolean> = _isEmpty
    
    fun loadFavoriteGames() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            try {
                val favorites = gameRepository.getFavoriteGames()
                _favoriteGames.value = favorites
                _isEmpty.value = favorites.isEmpty()
            } catch (e: Exception) {
                _error.value = e.message
                _isEmpty.value = true
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    fun refreshFavorites() {
        loadFavoriteGames()
    }
    
    fun removeFavorite(gameId: Int) {
        viewModelScope.launch {
            try {
                gameRepository.removeFavorite(gameId)
                loadFavoriteGames() // Refresh the list
            } catch (e: Exception) {
                _error.value = e.message
            }
        }
    }
}