package org.gua.gua.data.local.database

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.TypeConverter
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

@Entity(tableName = "favorite_games")
data class FavoriteGame(
    @PrimaryKey val id: Int,
    val name: String,
    val rating: Double?,
    val backgroundImage: String?,
    val addedAt: Long = System.currentTimeMillis()
)

@Entity(tableName = "history_games")
data class HistoryGame(
    @PrimaryKey val id: Int,
    val name: String,
    val rating: Double?,
    val backgroundImage: String?,
    val viewedAt: Long = System.currentTimeMillis()
)

@Entity(tableName = "cached_games")
data class CachedGame(
    @PrimaryKey val cacheKey: String,
    val data: String,
    val cachedAt: Long = System.currentTimeMillis(),
    val expiresAt: Long = System.currentTimeMillis() + (2 * 24 * 60 * 60 * 1000) // 2 days
)

class Converters {
    @TypeConverter
    fun fromStringList(value: List<String>): String {
        return Gson().toJson(value)
    }

    @TypeConverter
    fun toStringList(value: String): List<String> {
        return Gson().fromJson(value, object : TypeToken<List<String>>() {}.type)
    }
}