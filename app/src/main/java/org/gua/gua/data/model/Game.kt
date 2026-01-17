package org.gua.gua.data.model

import com.google.gson.annotations.SerializedName

data class Game(
    val id: Int,
    val name: String,
    val rating: Double?,
    @SerializedName("background_image")
    val backgroundImage: String?,
    val released: String?,
    val description: String?,
    val platforms: List<Platform>?,
    val genres: List<Genre>?,
    val developers: List<Developer>?,
    val publishers: List<Publisher>?,
    @SerializedName("metacritic")
    val metacriticScore: Int?
)

data class Platform(
    val id: Int,
    val name: String
)

data class Genre(
    val id: Int,
    val name: String
)

data class Developer(
    val id: Int,
    val name: String
)

data class Publisher(
    val id: Int,
    val name: String
)

data class GameResponse(
    val count: Int,
    val next: String?,
    val previous: String?,
    val results: List<Game>
)