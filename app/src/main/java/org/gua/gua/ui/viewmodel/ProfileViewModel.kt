package org.gua.gua.ui.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import org.gua.gua.data.local.UserPreferences
import org.gua.gua.data.model.Game
import org.gua.gua.data.model.User
import org.gua.gua.data.repository.GameRepository
import javax.inject.Inject

@HiltViewModel
class ProfileViewModel @Inject constructor(
    private val userPreferences: UserPreferences,
    private val gameRepository: GameRepository
) : ViewModel() {
    
    private val _userProfile = MutableLiveData<User?>()
    val userProfile: LiveData<User?> = _userProfile
    
    private val _userStats = MutableLiveData<UserStats?>()
    val userStats: LiveData<UserStats?> = _userStats
    
    private val _recentGames = MutableLiveData<List<Game>>()
    val recentGames: LiveData<List<Game>> = _recentGames
    
    fun loadUserProfile() {
        viewModelScope.launch {
            try {
                // Load user profile
                val user = userPreferences.getCurrentUser()
                _userProfile.value = user
                
                // Load user stats
                val stats = UserStats(
                    gamesViewed = gameRepository.getViewedGamesCount(),
                    favoritesCount = gameRepository.getFavoritesCount(),
                    reviewsCount = 0 // Placeholder
                )
                _userStats.value = stats
                
                // Load recent games
                val recentGames = gameRepository.getRecentlyViewedGames()
                _recentGames.value = recentGames
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
    
    fun logout() {
        userPreferences.logout()
        // Navigate back to login - handled by MainActivity
    }
    
    data class UserStats(
        val gamesViewed: Int,
        val favoritesCount: Int,
        val reviewsCount: Int
    )
}