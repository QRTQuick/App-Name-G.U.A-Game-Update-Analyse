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
class TrendingViewModel @Inject constructor(
    private val gameRepository: GameRepository
) : ViewModel() {
    
    private val _trendingGames = MutableLiveData<List<Game>>()
    val trendingGames: LiveData<List<Game>> = _trendingGames
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error
    
    private val _isEmpty = MutableLiveData<Boolean>()
    val isEmpty: LiveData<Boolean> = _isEmpty
    
    fun loadTrendingGames() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            try {
                when (val result = gameRepository.getTrendingGames()) {
                    is Resource.Success -> {
                        _trendingGames.value = result.data ?: emptyList()
                        _isEmpty.value = result.data.isNullOrEmpty()
                    }
                    is Resource.Error -> {
                        _error.value = result.message
                        _isEmpty.value = true
                    }
                    is Resource.Loading -> {
                        // Already handled above
                    }
                }
            } catch (e: Exception) {
                _error.value = e.message
                _isEmpty.value = true
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    fun refreshTrendingGames() {
        loadTrendingGames()
    }
}