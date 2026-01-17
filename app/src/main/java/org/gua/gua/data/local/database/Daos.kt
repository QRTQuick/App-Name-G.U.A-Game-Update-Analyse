package org.gua.gua.data.local.database

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface FavoriteDao {
    @Query("SELECT * FROM favorite_games ORDER BY addedAt DESC")
    fun getAllFavorites(): Flow<List<FavoriteGame>>
    
    @Query("SELECT * FROM favorite_games ORDER BY addedAt DESC")
    suspend fun getAllFavoritesList(): List<FavoriteGame>
    
    @Query("SELECT * FROM favorite_games WHERE id = :gameId")
    suspend fun getFavorite(gameId: Int): FavoriteGame?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun addFavorite(game: FavoriteGame)
    
    @Delete
    suspend fun removeFavorite(game: FavoriteGame)
    
    @Query("DELETE FROM favorite_games WHERE id = :gameId")
    suspend fun removeFavoriteById(gameId: Int)
    
    @Query("SELECT COUNT(*) FROM favorite_games")
    suspend fun getFavoritesCount(): Int
    
    @Query("DELETE FROM favorite_games")
    suspend fun clearAllFavorites()
}

@Dao
interface HistoryDao {
    @Query("SELECT * FROM history_games ORDER BY viewedAt DESC LIMIT 50")
    fun getHistory(): Flow<List<HistoryGame>>
    
    @Query("SELECT * FROM history_games ORDER BY viewedAt DESC LIMIT 50")
    suspend fun getHistoryList(): List<HistoryGame>
    
    @Query("SELECT * FROM history_games ORDER BY viewedAt DESC LIMIT :limit")
    suspend fun getRecentHistory(limit: Int): List<HistoryGame>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun addToHistory(game: HistoryGame)
    
    @Query("DELETE FROM history_games WHERE id = :gameId")
    suspend fun removeFromHistory(gameId: Int)
    
    @Query("DELETE FROM history_games")
    suspend fun clearHistory()
    
    @Query("SELECT COUNT(*) FROM history_games")
    suspend fun getHistoryCount(): Int
    
    @Query("DELETE FROM history_games WHERE id NOT IN (SELECT id FROM history_games ORDER BY viewedAt DESC LIMIT 50)")
    suspend fun trimHistory()
}

@Dao
interface CacheDao {
    @Query("SELECT * FROM cached_games WHERE cacheKey = :key AND expiresAt > :currentTime")
    suspend fun getCachedData(key: String, currentTime: Long = System.currentTimeMillis()): CachedGame?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun cacheData(cachedGame: CachedGame)
    
    @Query("DELETE FROM cached_games WHERE expiresAt <= :currentTime")
    suspend fun clearExpiredCache(currentTime: Long = System.currentTimeMillis())
    
    @Query("DELETE FROM cached_games")
    suspend fun clearAllCache()
    
    @Query("SELECT COUNT(*) FROM cached_games")
    suspend fun getCacheCount(): Int
    
    @Query("SELECT COUNT(*) FROM cached_games WHERE expiresAt <= :currentTime")
    suspend fun getExpiredCacheCount(currentTime: Long = System.currentTimeMillis()): Int
    
    @Query("SELECT SUM(LENGTH(data)) FROM cached_games")
    suspend fun getCacheSize(): Long
}