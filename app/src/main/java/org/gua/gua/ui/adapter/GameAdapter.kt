package org.gua.gua.ui.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.bumptech.glide.load.resource.drawable.DrawableTransitionOptions
import org.gua.gua.R
import org.gua.gua.data.model.Game
import org.gua.gua.databinding.ItemGameBinding

class GameAdapter(
    private val onGameClick: (Game) -> Unit
) : ListAdapter<Game, GameAdapter.GameViewHolder>(GameDiffCallback()) {
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): GameViewHolder {
        val binding = ItemGameBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return GameViewHolder(binding)
    }
    
    override fun onBindViewHolder(holder: GameViewHolder, position: Int) {
        holder.bind(getItem(position))
    }
    
    inner class GameViewHolder(
        private val binding: ItemGameBinding
    ) : RecyclerView.ViewHolder(binding.root) {
        
        fun bind(game: Game) {
            binding.apply {
                gameTitle.text = game.name
                gameRating.text = if (game.rating != null) {
                    "${game.rating}/5"
                } else {
                    "N/A"
                }
                
                // Load game image
                Glide.with(gameImage.context)
                    .load(game.backgroundImage)
                    .placeholder(R.drawable.placeholder_game)
                    .error(R.drawable.placeholder_game)
                    .transition(DrawableTransitionOptions.withCrossFade())
                    .into(gameImage)
                
                // Set click listener
                root.setOnClickListener {
                    onGameClick(game)
                }
            }
        }
    }
    
    private class GameDiffCallback : DiffUtil.ItemCallback<Game>() {
        override fun areItemsTheSame(oldItem: Game, newItem: Game): Boolean {
            return oldItem.id == newItem.id
        }
        
        override fun areContentsTheSame(oldItem: Game, newItem: Game): Boolean {
            return oldItem == newItem
        }
    }
}