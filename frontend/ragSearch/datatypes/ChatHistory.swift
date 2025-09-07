//
//  Product.swift
//  app
//
//  Created by Lucas Grant on 2025-08-01.
//

import Foundation
import SwiftData

struct Message: Codable {
    var role: String
    var content: String
}

struct ChatHistory: Codable {
    var messages: [Message]
}

//class MessageStorage {
//    var role: String
//    var content: String
//    
//    init(role: String, content: String) {
//        self.role = role
//        self.content = content
//    }
//    
//}
//
//@Model
//class ChatHistoryStorage {
//    var messages: [MessageStorage]
//    
//    init(messages: [MessageStorage]) {
//        self.messages = messages
//    }
//}
