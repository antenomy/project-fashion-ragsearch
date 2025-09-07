//
//  ProductBrowser.swift
//  ragSearch
//
//  Created by Lucas Grant on 2025-08-14.
//
import SwiftUI

let columns = [
    GridItem(.flexible()),
    GridItem(.flexible())
]

struct ProductBrowser: View {
    @Environment(\.modelContext) var modelContext
    
    @Binding var pageIndex: Int
    var productMatrix: [[Product]]
    let titleText: String
    let favourites: [Favourite]
    
    init(
        productMatrix: [[Product]] = [],
        titleText: String,
        pageIndex: Binding<Int>,
        favourites: [Favourite]
    ) {
        self.productMatrix = productMatrix
        self.titleText = titleText
        self._pageIndex = pageIndex
        self.favourites = favourites
    }
    
    var body: some View {
        ZStack {
            if productMatrix.count > 0 {
                ScrollView { //scrollProxy in
                    Text(titleText)
                        .basicText(size: 24)
                    
                    VStack {
                        
                        
                        if productMatrix.count > 0 {
                            LazyVGrid(columns: columns, spacing: 0) {
                                ForEach(productMatrix[pageIndex], id: \.articleId) {product in
                                    ProductTile(
                                        product,
                                        columnCount: 2
                                    )
                                    .padding(.vertical, 4)
                                    
                                }
                            }
                            
                            HStack {
                                Button(action: {
                                    if pageIndex > 0 {
                                        pageIndex -= 1
                                    }
                                }) {
                                    CircleButton(icon: "chevron.left")
                                }
                                .opacity(pageIndex > 0 ? 1 : 0)
                                
                                Text("Page \(pageIndex + 1)")
                                    .basicText(size: 24)
                                
                                Button(action: {
                                    if pageIndex + 1 < productMatrix.count {
                                        pageIndex += 1
                                    }
                                }) {
                                    CircleButton(icon: "chevron.right")
                                }
                                .opacity(pageIndex < productMatrix.count ? 1 : 0)
                            }
                            .padding(.bottom, 96)
                        }
                    }
                }
                .padding(.horizontal, 4)
            } else {
                VStack {
                    Text(titleText)
                        .basicText(size: 24)
                    Spacer()
                }
                
                VStack {
                    Spacer()
                    Text("Loading...")
                        .basicText(size: 16)
                    ProgressView()
                        .tint(.white)
                    Spacer()
                }
                
            }
        }
    }
}
