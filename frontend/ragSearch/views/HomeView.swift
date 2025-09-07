//
//  HomeView.swift
//  app
//
//  Created by Lucas Grant on 2025-07-25.
//

import SwiftUI

struct HomeView : View {
    @ObservedObject var viewModel: SharedViewModel
    
    init(_ viewModel: SharedViewModel) {
        self.viewModel = viewModel
    }
    
    var body: some View {
        VStack (alignment: .leading) {
            HStack {
                Text("HOME")
                    .basicText(size: 48)
                    .padding()
            }
            .frame(maxWidth: .infinity)
            
            Spacer()
            
            MenuButton(text: "Conversation", action: {viewModel.currentView = .conversation})
                .padding(.horizontal, 32)
            
            MenuButton(text: "Products", action: {viewModel.currentView = .product})
                .padding(.horizontal, 32)
            
            MenuButton(text: "Favourites", action: {viewModel.currentView = .favourites})
                .padding(.horizontal, 32)
            
            MenuButton(text: "Outfit", action: {viewModel.currentView = .outfit})
                .padding(.horizontal, 32)
            
            MenuButton(text: "Settings", action: {viewModel.currentView = .admin})
                .padding(.horizontal, 32)
            
            Spacer()
            
            
        }
        .padding(.bottom)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

#Preview {
    ContentView()
}
