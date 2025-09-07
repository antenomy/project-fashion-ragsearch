//
//  SelectFavouriteSubView.swift
//  app
//
//  Created by Lucas Grant on 2025-07-26.
//

import SwiftUI

struct SelectFavourite: View {
//    @Binding var keepViewOpen: Bool
    var dismissAction: () -> Void
    
    
    
    var body: some View {
        ZStack {
            VStack {
               Spacer()
                HStack {
                    Spacer()
                    Button(action: dismissAction) {
                        Image(systemName: "arrow.down.right.and.arrow.up.left")
                        .font(.system(size: 16))
                        .fontWeight(.bold)
                        .foregroundColor(CustomColor.white)
//                        .frame(width: 40, height: 40)
//                        Label("", systemImage: "arrow.down.right.and.arrow.up.left")
//                            .basicText(size: 18)
                    }
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .roundedBox()
            .padding(.horizontal)
//            .padding(.vertical, )
            .onSwipe(down: dismissAction)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color.black.opacity(0.4))
    }
}

#Preview {
    ContentView(.conversation)
}
