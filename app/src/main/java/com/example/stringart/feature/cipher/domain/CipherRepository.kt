package com.example.stringart.feature.cipher.domain

import kotlinx.coroutines.flow.Flow

interface CipherRepository {
    val mapping: Flow<Map<String, String>>
    suspend fun saveMapping(mapping: Map<String, String>)
    suspend fun resetDefault()
}
