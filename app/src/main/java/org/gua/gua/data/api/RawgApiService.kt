package org.gua.gua.data.api

import org.gua.gua.data.model.Game
import org.gua.gua.data.model.GameResponse
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

interface RawgApiService {
    
    @GET("games")
    suspend fun getGames(
        @Query("key") apiKey: String,
        @Query("page_size") pageSize: Int = 10,
        @Query("ordering") ordering: String? = null,
        @Query("search") search: String? = null,
        @Query("page") page: Int = 1
    ): Response<GameResponse>
    
    @GET("games/{id}")
    suspend fun getGameDetails(
        @Path("id") gameId: Int,
        @Query("key") apiKey: String
    ): Response<Game>
}