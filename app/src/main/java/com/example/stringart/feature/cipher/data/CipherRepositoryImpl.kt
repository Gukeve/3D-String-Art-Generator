package com.example.stringart.feature.cipher.data

import com.example.stringart.feature.cipher.domain.CipherDefaults
import com.example.stringart.feature.cipher.domain.CipherRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class CipherRepositoryImpl(private val store: CipherMappingStore) : CipherRepository {
    override val mapping: Flow<Map<String, String>> = store.mappingFlow.map { if (it.isEmpty()) CipherDefaults.defaultMap else it }
    override suspend fun saveMapping(mapping: Map<String, String>) = store.save(mapping)
    override suspend fun resetDefault() = store.save(CipherDefaults.defaultMap)
}
