//
//  TextBox.swift
//  ragSearch
//
//  Created by Lucas Grant on 2025-08-11.
//

import SwiftUI

struct TextBox: View {
    let message : String
    
    let cornerRadius = CGFloat(20)
    
    let roundingCorners: UIRectCorner
    let author_role: String

    
    init(message: String,
         author_role: String
    ) {
        self.message = message
        self.roundingCorners = (author_role == "user") ? [.topLeft, .topRight, .bottomLeft] : [.topLeft, .topRight, .bottomRight]
        self.author_role = author_role
    }
    
    var body: some View {
        HStack {
            if author_role == "user" {
                Spacer()
            }
            
            Text(message)
                .padding(16)
                .basicText(size: 14)
                .background(CustomColor.gray)
                .clipShape(RoundedCornerShape(radius: cornerRadius, corners: roundingCorners))
                .padding(.vertical, 8)
                .padding(.leading, (author_role == "user") ? 36 : 4)
                .padding(.trailing, (author_role == "user") ? 4 : 36)
            
            if author_role != "user" {
                Spacer()
            }
        }
    }
}

#Preview {
    ContentView(.product)
}
