//
//  ProductStruct.swift
//  app
//
//  Created by Lucas Grant on 2025-07-25.
//

import SwiftUI
import SwiftData

//enum tileSize {
//    case large
//    .small
//    
//}

struct ProductTile: View {
    @Environment(\.modelContext) var modelContext
    @Query private var favourites: [Favourite]
    
    var favourited: Bool {
        favourites.contains { $0.articleId == productItem.articleId }
    }
    
    var productItem : Product
    let columnCount : Int
    
    let nameText : String
    let sizeText : String
    let cleanedImgUrl: String
    
    let cornerRadius = CGFloat(20)
    let paddingWidth : CGFloat
    let nameTextSize : CGFloat
    let imageAspectRatio: Double = 1.5 //1.111111
    
    init(_  productItem: Product,
            columnCount : Int = 1
    ) {
        self.productItem = productItem
        self.columnCount = columnCount
        self.cleanedImgUrl = productItem.imageUrl.replacingOccurrences(of: "_xs-1.jpg?ver=1", with: "").replacingOccurrences(of: "_xs-1.jpg?ver=2", with: "").replacingOccurrences(of: "_xs-1.jpg?ver=3", with: "")
        
        // Name
        let placeholderName = productItem.name
        var shortNameText = ""
        var longNameText = ""
        
        if let slashIndex = placeholderName.firstIndex(of: "/") {
            shortNameText = String(placeholderName[..<slashIndex])
            longNameText = String(placeholderName[placeholderName.index(after: slashIndex)...]).trimmingCharacters(in: .whitespaces)
        } else {
            shortNameText = placeholderName.trimmingCharacters(in: .whitespaces)
            longNameText = placeholderName.trimmingCharacters(in: .whitespaces)
        }
        
        if columnCount == 1 {
            self.nameText = longNameText.uppercased()
            self.paddingWidth = 16
            self.nameTextSize = 36
        } else {
            self.nameText = shortNameText.uppercased() //shortNameText.uppercased()
            self.paddingWidth = 8
            self.nameTextSize = 18
        }

        
        // Size
        let placeholderSize = productItem.size
        
        if let placeholderSize {
            if placeholderSize.count > 1 {
                self.sizeText = "\(placeholderSize.first ?? "XS")-\(placeholderSize.last ?? "XL")"
            } else if placeholderSize.count == 1 {
                if let identifier = placeholderSize.first {
                    if identifier != "" {
                        self.sizeText = "One Size"
                    } else {
                        self.sizeText = identifier
                    }
                } else {
                    self.sizeText = "One Size"
                }
            } else {
                self.sizeText = "One Size"
            }
        } else {
            self.sizeText = "One Size"

        }
    }
    
    var body: some View {
        VStack(spacing: 12){
            ZStack {
                GeometryReader { geo in
                    AsyncImage(url: URL(string: cleanedImgUrl)) { image in
                        image
                            .resizable()
                            .scaledToFill()
                            .frame(width: geo.size.width, height: geo.size.width * imageAspectRatio)
                            .aspectRatio(1, contentMode: .fit)
                            .clipped()
                            .overlay() {
                                VStack {
                                    Spacer()
                                    HStack {
                                        Spacer()
                                        Button(action: {
                                            if favourited {
                                                let predicate = #Predicate<Favourite> { fav in
                                                    fav.articleId == productItem.articleId
                                                }
                                                let descriptor = FetchDescriptor<Favourite>(predicate: predicate)

                                                do {
                                                    let results = try modelContext.fetch(descriptor)
                                                    for fav in results {
                                                        modelContext.delete(fav)
                                                    }
                                                    try modelContext.save()
                                                } catch {
                                                    print("Failed to delete favourite: \(error)")
                                                }
                                            } else {
                                                modelContext.insert(Favourite(articleId: productItem.articleId))
                                                
                                                do {
                                                    try modelContext.save()
                                                } catch {
                                                    print("Failed to save: \(error.localizedDescription)")
                                                }
                                            }
                                        }){
                                            if favourited {
                                                Image(systemName: "star.fill")
                                                    .padding(8)
                                                    .foregroundColor(Color.yellow)
                                            } else {
                                                Image(systemName: "star")
                                                    .padding(8)
                                                    .foregroundColor(CustomColor.lightGray)
                                            }
                                        }
                                    }
                                }
                            }
                        //RoundedSquare(cornerRadius: cornerRadius))
                    } placeholder: {
                        ZStack {
                            Image("placeholder")
                                .resizable()
                                .scaledToFill()
                                .frame(width: geo.size.width, height: geo.size.width * imageAspectRatio)
                                .aspectRatio(1, contentMode: .fill)
                                .clipped()
                            ProgressView()
                                .tint(.white)
                        }
                    }
                }
            }
            .aspectRatio((1 / imageAspectRatio), contentMode: .fit)
//            .overlay(
//                RoundedRectangle(cornerRadius: cornerRadius)
//                    .stroke(CustomColor.lightGray, lineWidth: 2)
//            )

            HStack {
                Spacer()
                Text(nameText)
                    .basicText(size: nameTextSize)
                Spacer()
            }
            
            HStack {
                Text("£ \(String(format: "%.2f", productItem.price))")
                    .basicText(size: 16)//nameTextSize * 0.8)
//                    .padding(.leading, paddingWidth * 2)
//                Spacer()
//                Text(sizeText)
//                    .basicText(size: 16)
//                    .padding(.trailing, paddingWidth * 2)
            }
//            .padding(.top, 1)//paddingWidth * 0.25)
//            .padding(.bottom, paddingWidth * 2)
            

        }
        .padding(.bottom, paddingWidth * 2)
        .roundedBox(paddingOn: false)
    }
}

#Preview {
    ContentView(.product)
}
