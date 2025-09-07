//
//  Responses.swift
//  ragSearch
//
//  Created by Lucas Grant on 2025-08-11.
//

import Foundation

struct Conversation : Codable {
    var chatMessages: ChatHistory
    var systemRecommendations: [Reccomendation]
}

