package org.gua.gua.ui

import android.os.Bundle
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.setupWithNavController
import com.google.android.material.bottomnavigation.BottomNavigationView
import dagger.hilt.android.AndroidEntryPoint
import org.gua.gua.R
import org.gua.gua.databinding.ActivityMainBinding
import org.gua.gua.ui.viewmodel.MainViewModel

@AndroidEntryPoint
class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    private val viewModel: MainViewModel by viewModels()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupNavigation()
        observeViewModel()
    }
    
    private fun setupNavigation() {
        val navHostFragment = supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
        val navController = navHostFragment.navController
        
        binding.bottomNavigation.setupWithNavController(navController)
        
        // Handle navigation based on user state
        viewModel.checkUserState()
    }
    
    private fun observeViewModel() {
        viewModel.navigationEvent.observe(this) { destination ->
            val navHostFragment = supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
            val navController = navHostFragment.navController
            
            when (destination) {
                "disclaimer" -> navController.navigate(R.id.disclaimerFragment)
                "login" -> navController.navigate(R.id.loginFragment)
                "home" -> navController.navigate(R.id.homeFragment)
            }
        }
        
        viewModel.showBottomNav.observe(this) { show ->
            binding.bottomNavigation.visibility = if (show) {
                BottomNavigationView.VISIBLE
            } else {
                BottomNavigationView.GONE
            }
        }
    }
}