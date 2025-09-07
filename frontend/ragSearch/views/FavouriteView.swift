//
//  AdminView.swift
//  app
//
//  Created by Lucas Grant on 2025-07-25.
//

import SwiftUI
import SwiftData

struct FavouriteView : View {
    @ObservedObject var viewModel: SharedViewModel
    
    @Environment(\.modelContext) var modelContext
    @Query var favourites: [Favourite]
    
    private let productsPerPage = 30
    @State private var pageIndex = 0
    
    @State private var loadedProducts: [[Product]] = []
    @State private var loadedProductIds: [String] = []
    
    
    init(_ viewModel: SharedViewModel) {
        self.viewModel = viewModel
    }
    
    var body: some View {
        ProductBrowser(
            productMatrix: loadedProducts,
            titleText: "FAVOURITES",
            pageIndex: $pageIndex,
            favourites: favourites
        )
        .onAppear{
            Task {
                var newProductArrays: [[Product]] = []
                var currentProductArray: [Product] = []
                
                for favourite in favourites {
                    if currentProductArray.count >= productsPerPage {
                        newProductArrays.append(currentProductArray)
                        currentProductArray = []
                    }
                    
                    do {
                        if let product = try await ItemHandler.getItemFromId(articleId: favourite.articleId) {
                            currentProductArray.append(product)
                        }
                    } catch {
                        print("Failed to load product for \(favourite.articleId): \(error)")
                    }
                }
                
                if !currentProductArray.isEmpty {
                    newProductArrays.append(currentProductArray)
                }
                
                loadedProducts = newProductArrays
            }
            
//            if let lastProductPage = loadedProducts.popLast() {
//                if lastProductPage.count <= productsPerPage {
//                    currentProductArray = lastProductPage
//                } else {
//                    loadedProducts.append(lastProductPage)
//                }
//            }
//            
//            Task {
//                for favourite in favourites {
//                    if currentProductArray.count >= productsPerPage {
//                        newProductArrays.append(currentProductArray)
//                        currentProductArray = []
//                    }
//                    
//                    let requestedItem = try await ItemHandler.getItemFromId(articleId: favourite.articleId)
//                    
//                    if let identifier = requestedItem  {
//                        currentProductArray.append(identifier)
//                    }
//                }
//            }
        }
    }
}
