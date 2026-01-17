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
class HomeViewModel @Inject constructor(
    private val gameRepository: GameRepository
) : ViewModel() {
    
    private val _games = MutableLiveData<List<Game>>()
    val games: LiveData<List<Game>> = _games
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error
    
    private val _isEmpty = MutableLiveData<Boolean>()
    val isEmpty: LiveData<Boolean> = _isEmpty
    
    fun loadLatestGames() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            when (val result = gameRepository.getGames(
                pageSize = 10,
                ordering = "-added" // Latest games
            )) {
                is Resource.Success -> {
                    val gameList = result.data?.results ?: emptyList()
                    _games.value = gameList
                    _isEmpty.value = gameList.isEmpty()
                }
                is Resource.Error -> {
                    _error.value = result.message
                    _isEmpty.value = _games.value?.isEmpty() ?: true
                }
                is Resource.Loading -> {
                    // Already handled above
                }
            }
            
            _isLoading.value = false
        }
    }
    
    fun refreshGames() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            when (val result = gameRepository.getGames(
                pageSize = 10,
                ordering = "-added",
                useCache = false // Force refresh
            )) {
                is Resource.Success -> {
                    val gameList = result.data?.results ?: emptyList()
                    _games.value = gameList
                    _isEmpty.value = gameList.isEmpty()
                }
                is Resource.Error -> {
                    _error.value = result.message
                }
                is Resource.Loading -> {
                    // Already handled above
                }
            }
            
            _isLoading.value = false
        }
    }
}