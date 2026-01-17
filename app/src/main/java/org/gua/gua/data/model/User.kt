package org.gua.gua.data.model

data class User(
    val username: String,
    val email: String,
    val disclaimerAccepted: Boolean = false
)

data class UserStats(
    val viewed: Int = 0,
    val favorites: Int = 0,
    val reviews: Int = 0
)