//
//  ProductView.swift
//  app
//
//  Created by Lucas Grant on 2025-07-25.
//

import SwiftUI
import SwiftData

struct ProductView : View {
    @ObservedObject var viewModel: SharedViewModel
    
    private let productsPerPage = 30
    
    @State private var pageIndex = 0
    
    @State private var loadedProducts: [[Product]] = []
    @State private var loadedProductIds: [String] = []
    
//    @Environment(\.modelContext) var modelContext
    @Query var favourites: [Favourite]
    
    init(_ viewModel: SharedViewModel) {
        self.viewModel = viewModel
    }

    var body: some View {
        ZStack {
            ProductBrowser(
                productMatrix: loadedProducts,
                titleText: "PRODUCT",
                pageIndex: $pageIndex,
                favourites: favourites
            )
        }
        .onAppear() {
            Task {
                for iteration in Range(0 ... 5) {
                    let products = try await ItemHandler.getCount(count: productsPerPage , pageNumber: iteration)
                    
                    if let new_products = products {
                        loadedProducts.append(new_products)
                        
                        for product in new_products {
                            loadedProductIds.append(product.articleId)
                        }
                    }
                }
            }
        }
    }
}

#Preview {
    ContentView(.product)
}



//            .onAppear() {
//                withAnimation {
//                    scrollProxy.scrollTo("TOP", anchor: .top)
//                }
//            }


//                        withAnimation {
//                            scrollProxy.scrollTo("TOP", anchor: .top)
//                        }
