//
//  InputField.swift
//  app
//
//  Created by Lucas Grant on 2025-07-25.
//
import SwiftUI

struct MenuButton: View {
    let text: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            ZStack {
                Text(text)
                    .basicText(size: 36)
//                    .padding()
            }
//            .frame(maxWidth: .infinity)
            
        }
//        .background(CustomColor.gray)
//        .cornerRadius(10)
//        .overlay(
//            RoundedRectangle(cornerRadius: 10)
//                .stroke(CustomColor.lightGray, lineWidth: 2)
//        )
//        .padding()
    }
}

#Preview {
    ContentView()
}
