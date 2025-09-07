//
//  Product.swift
//  app
//
//  Created by Lucas Grant on 2025-08-01.
//

import Foundation

struct Product: Codable {
    var id: Int?
    var articleId: String
    var name: String
    var imageUrl: String
    var price: Double

    var productType: String
    var productGroup: String?

    var externalBrand: String?
    var productDescription: String?
    var jsonDescription: String?

    var color: [String]?
    var size: [String]?

    var embedding: [Double]?
}
