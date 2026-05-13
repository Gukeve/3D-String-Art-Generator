package com.example.stringart.feature.cipher.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.stringart.feature.cipher.domain.CipherDefaults
import com.example.stringart.feature.cipher.domain.CipherEngine
import com.example.stringart.feature.cipher.domain.CipherRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class CipherUiState(
    val input: String = "",
    val output: String = "",
    val mapping: Map<String, String> = CipherDefaults.defaultMap,
    val error: String? = null
)

class CipherViewModel(private val repo: CipherRepository) : ViewModel() {
    private val engine = CipherEngine()
    private val _ui = MutableStateFlow(CipherUiState())
    val ui: StateFlow<CipherUiState> = _ui.asStateFlow()

    init { viewModelScope.launch { repo.mapping.collect { _ui.update { s -> s.copy(mapping = it) } } } }
    fun setInput(v: String) = _ui.update { it.copy(input = v) }
    fun clear() = _ui.update { it.copy(input = "", output = "", error = null) }
    fun encrypt() = transform(true)
    fun decrypt() = transform(false)

    private fun transform(isEncrypt: Boolean) {
        val text = _ui.value.input
        if (text.length > CipherDefaults.MAX_LENGTH) {
            _ui.update { it.copy(error = "Limit ${CipherDefaults.MAX_LENGTH}") }
            return
        }
        val out = if (isEncrypt) engine.encrypt(text, _ui.value.mapping) else engine.decrypt(text, _ui.value.mapping)
        _ui.update { it.copy(output = out, error = null) }
    }

    fun updateMapping(k: String, v: String) = viewModelScope.launch { repo.saveMapping(_ui.value.mapping + (k to v)) }
    fun removeMapping(k: String) = viewModelScope.launch { repo.saveMapping(_ui.value.mapping - k) }
    fun resetDefault() = viewModelScope.launch { repo.resetDefault() }
}
