//
//  ItemHandler.swift
//  ragSearch
//
//  Created by Lucas Grant on 2025-08-01.
//

import SwiftUI

struct ItemHandler {
    static func getAllItems() async throws -> [Product]? {
        let endpoint = Const.endpointAdress + "/database/get_all"
        let url = try ItemHandler.getURL(endpoint, callFunction: "Get All Items")
        
        let (data, response) = try await URLSession.shared.data(from: url)
        
        if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode != 200 {
            throw GetItemError.invalidResponse
        }
        
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            return try decoder.decode([Product].self, from: data)
        } catch {
            print("Error while running getAllItems")
            print(error)
        }
        return nil
    }

    static func getItemFromId(articleId: String) async throws -> Product? {
        let endpoint = Const.endpointAdress + "/database/id_get/\(articleId)"
        let url = try ItemHandler.getURL(endpoint, callFunction: "Get Item From ID")
        
        let (data, response) = try await URLSession.shared.data(from: url)
        
        if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode != 200 {
            throw GetItemError.invalidResponse
        }
        
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            return try decoder.decode(Product.self, from: data)
        } catch {
            print("Error while running getAllItems")
            print(error)
        }
        return nil
    }

    
    static func getCount(count: Int, pageNumber: Int = 0) async throws -> [Product]? {
        print("loading products...")
        
        let endpoint = Const.endpointAdress + "/database/get_count/page\(pageNumber)/\(count)"
        let url = try ItemHandler.getURL(endpoint, callFunction: "Get a Number of Items")
        
        let (data, response) = try await URLSession.shared.data(from: url)
        
        print(response)
        
        if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode != 200 {
            throw GetItemError.invalidResponse
        }
        
        print("recieved products...")
        
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            print("decoded products...")
            return try decoder.decode([Product].self, from: data)
        } catch {
            print("Error while running getAllItems")
            print(error)
        }
        return nil
    }

    static func reccomendationsFromPrompt(_ chatHistory: ChatHistory) async throws -> [Reccomendation]? {
        let endpoint = Const.endpointAdress + "/recommend_products"
        let url = try ItemHandler.getURL(endpoint, callFunction: "Get Recommendations from Prompt")
        
        var request = URLRequest(url: url)
        let encoder = JSONEncoder()
        encoder.keyEncodingStrategy = .convertToSnakeCase
        
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            let jsonData = try encoder.encode(chatHistory)
            request.httpBody = jsonData
        } catch {
            throw EditItemError.encodingFailed(error)
        }
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        var reccomendations: [Reccomendation]? = nil
    
        do {
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            reccomendations = try decoder.decode([Reccomendation].self, from: data)
        } catch {
            throw error
        }
        
        if let httpResponse = response as? HTTPURLResponse {
            switch httpResponse.statusCode {
            case 200...299:
                return reccomendations
            default:
                throw EditItemError.invalidResponse(httpResponse.statusCode)
            }
        }
        
        return nil
    }

    private static func getURL(_ endpoint: String, callFunction: String) throws -> URL {
        guard let url = URL(string: endpoint) else {
            print(callFunction, "invalidURL")
            throw ItemHandlerError.invalidURL
        }
        return url
    }
}
