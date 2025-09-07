//
//  Favourite.swift
//  ragSearch
//
//  Created by Lucas Grant on 2025-08-14.
//

import SwiftData

@Model
class Favourite {
    var articleId: String
    
    init(articleId: String) {
        self.articleId = articleId
    }
}
