package com.plcoding.stockmarketapp.data.remote
import retrofit2.http.Query

interface StockApi {

    @GET( value: "query?function=LISTING_STATUS")
    suspend fun getListings(
        @Query( value: "apikey") apiKey: String
    ): ResponseBody

    companion object {
        const val API_KEY = "U6Q5OVT6QPMC2IOE"
        const val BASE_URL = "https://alphavantage.co"
    }
}