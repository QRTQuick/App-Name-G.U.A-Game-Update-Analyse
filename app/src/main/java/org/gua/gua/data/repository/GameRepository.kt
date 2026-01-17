package org.gua.gua.data.repository

import kotlinx.coroutines.flow.Flow
import org.gua.gua.data.api.RawgApiService
import org.gua.gua.data.local.database.*
import org.gua.gua.data.model.Game
import org.gua.gua.data.model.GameResponse
import org.gua.gua.utils.Resource
import com.google.gson.Gson
import java.security.MessageDigest
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class GameRepository @Inject constructor(
    private val apiService: RawgApiService,
    private val favoriteDao: FavoriteDao,
    private val historyDao: HistoryDao,
    private val cacheDao: CacheDao
) {
    
    companion object {
        private const val API_KEY = "22413e93d24a4e05a6da4992ea2769ee" // Fallback API key
    }
    
    suspend fun getGames(
        pageSize: Int = 10,
        ordering: String? = null,
        search: String? = null,
        page: Int = 1,
        useCache: Boolean = true
    ): Resource<GameResponse> {
        val cacheKey = generateCacheKey("games", mapOf(
            "pageSize" to pageSize.toString(),
            "ordering" to (ordering ?: ""),
            "search" to (search ?: ""),
            "page" to page.toString()
        ))
        
        // Try cache first
        if (useCache) {
            val cachedData = cacheDao.getCachedData(cacheKey)
            if (cachedData != null) {
                val gameResponse = Gson().fromJson(cachedData.data, GameResponse::class.java)
                return Resource.Success(gameResponse)
            }
        }
        
        // Fetch from API
        return try {
            val response = apiService.getGames(API_KEY, pageSize, ordering, search, page)
            if (response.isSuccessful && response.body() != null) {
                val gameResponse = response.body()!!
                
                // Cache the response
                val cachedGame = CachedGame(
                    cacheKey = cacheKey,
                    data = Gson().toJson(gameResponse)
                )
                cacheDao.cacheData(cachedGame)
                
                Resource.Success(gameResponse)
            } else {
                Resource.Error("Failed to fetch games: ${response.message()}")
            }
        } catch (e: Exception) {
            Resource.Error("Network error: ${e.message}")
        }
    }
    
    suspend fun getGameDetails(gameId: Int, useCache: Boolean = true): Resource<Game> {
        val cacheKey = generateCacheKey("game_details", mapOf("id" to gameId.toString()))
        
        // Try cache first
        if (useCache) {
            val cachedData = cacheDao.getCachedData(cacheKey)
            if (cachedData != null) {
                val game = Gson().fromJson(cachedData.data, Game::class.java)
                return Resource.Success(game)
            }
        }
        
        // Fetch from API
        return try {
            val response = apiService.getGameDetails(gameId, API_KEY)
            if (response.isSuccessful && response.body() != null) {
                val game = response.body()!!
                
                // Cache the response
                val cachedGame = CachedGame(
                    cacheKey = cacheKey,
                    data = Gson().toJson(game)
                )
                cacheDao.cacheData(cachedGame)
                
                // Add to history
                addToHistory(game)
                
                Resource.Success(game)
            } else {
                Resource.Error("Failed to fetch game details: ${response.message()}")
            }
        } catch (e: Exception) {
            Resource.Error("Network error: ${e.message}")
        }
    }
    
    // Favorites
    fun getFavorites(): Flow<List<FavoriteGame>> = favoriteDao.getAllFavorites()
    
    suspend fun addToFavorites(game: Game) {
        val favoriteGame = FavoriteGame(
            id = game.id,
            name = game.name,
            rating = game.rating,
            backgroundImage = game.backgroundImage
        )
        favoriteDao.addFavorite(favoriteGame)
    }
    
    suspend fun removeFromFavorites(gameId: Int) {
        favoriteDao.removeFavoriteById(gameId)
    }
    
    suspend fun isFavorite(gameId: Int): Boolean {
        return favoriteDao.getFavorite(gameId) != null
    }
    
    suspend fun getFavoritesCount(): Int = favoriteDao.getFavoritesCount()
    
    // History
    fun getHistory(): Flow<List<HistoryGame>> = historyDao.getHistory()
    
    private suspend fun addToHistory(game: Game) {
        val historyGame = HistoryGame(
            id = game.id,
            name = game.name,
            rating = game.rating,
            backgroundImage = game.backgroundImage
        )
        historyDao.addToHistory(historyGame)
        historyDao.trimHistory() // Keep only last 50
    }
    
    suspend fun clearHistory() = historyDao.clearHistory()
    
    suspend fun getHistoryCount(): Int = historyDao.getHistoryCount()
    
    // Cache management
    suspend fun clearExpiredCache() = cacheDao.clearExpiredCache()
    
    suspend fun clearAllCache() = cacheDao.clearAllCache()
    
    suspend fun getCacheCount(): Int = cacheDao.getCacheCount()
    
    suspend fun getExpiredCacheCount(): Int = cacheDao.getExpiredCacheCount()
    
    // Additional methods for ViewModels
    suspend fun searchGames(query: String): Resource<List<Game>> {
        val response = getGames(search = query, pageSize = 20)
        return when (response) {
            is Resource.Success -> Resource.Success(response.data?.results ?: emptyList())
            is Resource.Error -> Resource.Error(response.message ?: "Search failed")
            is Resource.Loading -> Resource.Loading()
        }
    }
    
    suspend fun getTrendingGames(): Resource<List<Game>> {
        val response = getGames(ordering = "-rating", pageSize = 20)
        return when (response) {
            is Resource.Success -> Resource.Success(response.data?.results ?: emptyList())
            is Resource.Error -> Resource.Error(response.message ?: "Failed to load trending games")
            is Resource.Loading -> Resource.Loading()
        }
    }
    
    suspend fun getLatestGames(): Resource<List<Game>> {
        val response = getGames(ordering = "-released", pageSize = 20)
        return when (response) {
            is Resource.Success -> Resource.Success(response.data?.results ?: emptyList())
            is Resource.Error -> Resource.Error(response.message ?: "Failed to load latest games")
            is Resource.Loading -> Resource.Loading()
        }
    }
    
    suspend fun getFavoriteGames(): List<Game> {
        val favorites = favoriteDao.getAllFavoritesList()
        return favorites.map { favorite ->
            Game(
                id = favorite.id,
                name = favorite.name,
                rating = favorite.rating,
                backgroundImage = favorite.backgroundImage,
                released = "",
                platforms = emptyList(),
                genres = emptyList(),
                developers = emptyList(),
                publishers = emptyList(),
                description = ""
            )
        }
    }
    
    suspend fun getGameHistory(): List<Game> {
        val history = historyDao.getHistoryList()
        return history.map { historyItem ->
            Game(
                id = historyItem.id,
                name = historyItem.name,
                rating = historyItem.rating,
                backgroundImage = historyItem.backgroundImage,
                released = "",
                platforms = emptyList(),
                genres = emptyList(),
                developers = emptyList(),
                publishers = emptyList(),
                description = ""
            )
        }
    }
    
    suspend fun getRecentlyViewedGames(): List<Game> {
        val recent = historyDao.getRecentHistory(5)
        return recent.map { historyItem ->
            Game(
                id = historyItem.id,
                name = historyItem.name,
                rating = historyItem.rating,
                backgroundImage = historyItem.backgroundImage,
                released = "",
                platforms = emptyList(),
                genres = emptyList(),
                developers = emptyList(),
                publishers = emptyList(),
                description = ""
            )
        }
    }
    
    suspend fun addFavorite(game: Game) = addToFavorites(game)
    
    suspend fun removeFavorite(gameId: Int) = removeFromFavorites(gameId)
    
    suspend fun addToHistory(game: Game) {
        val historyGame = HistoryGame(
            id = game.id,
            name = game.name,
            rating = game.rating,
            backgroundImage = game.backgroundImage
        )
        historyDao.addToHistory(historyGame)
        historyDao.trimHistory()
    }
    
    suspend fun getViewedGamesCount(): Int = historyDao.getHistoryCount()
    
    suspend fun refreshCache() {
        clearExpiredCache()
        // Refresh popular games cache
        getLatestGames()
        getTrendingGames()
    }
    
    suspend fun clearCache() = clearAllCache()
    
    suspend fun getCacheSize(): Long {
        return cacheDao.getCacheSize()
    }
    
    private fun generateCacheKey(endpoint: String, params: Map<String, String>): String {
        val paramString = params.entries.sortedBy { it.key }.joinToString("&") { "${it.key}=${it.value}" }
        val input = "$endpoint?$paramString"
        return MessageDigest.getInstance("MD5").digest(input.toByteArray()).joinToString("") { "%02x".format(it) }
    }
}