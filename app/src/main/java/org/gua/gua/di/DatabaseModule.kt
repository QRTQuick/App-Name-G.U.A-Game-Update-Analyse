package org.gua.gua.di

import android.content.Context
import androidx.room.Room
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import org.gua.gua.data.local.database.*
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    
    @Provides
    @Singleton
    fun provideGameDatabase(@ApplicationContext context: Context): GameDatabase {
        return Room.databaseBuilder(
            context.applicationContext,
            GameDatabase::class.java,
            "game_database"
        ).build()
    }
    
    @Provides
    fun provideFavoriteDao(database: GameDatabase): FavoriteDao = database.favoriteDao()
    
    @Provides
    fun provideHistoryDao(database: GameDatabase): HistoryDao = database.historyDao()
    
    @Provides
    fun provideCacheDao(database: GameDatabase): CacheDao = database.cacheDao()
}