//
//  ContentView.swift
//  Project
//
//  Created by Lucas Grant on 2025-07-02.
//

import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel: SharedViewModel
    
    init(_ currentView: CurrentView = .home) {
        _viewModel = StateObject(wrappedValue: SharedViewModel(startView: currentView))
    }
    
    var body: some View {
        ZStack {
            
            // Background
            RadialGradient(
                gradient: Gradient(colors: [CustomColor.purple, CustomColor.darkGray]),
                center: .bottom,
                startRadius: 0,
                endRadius: 400
            )
            .edgesIgnoringSafeArea(.all)
            
            // Main Navigation Stack
            VStack {
                switch viewModel.currentView {
            
                    case .home:
                        HomeView(viewModel)

                    case .admin:
                        AdminView(viewModel)
                        
                    case .product:
                        ProductView(viewModel)
                    case .conversation:
                        ConversationView(viewModel)
                    
                    case .favourites:
                        FavouriteView(viewModel)
                        
                    case .outfit:
                        OutfitView(viewModel)

                    case .menu:
                        Text("build menu placeholder view")
                            .basicText(size: 16)
                }
            }
            if viewModel.showMenuSlider {
                MenuSlider(
                    viewModel: viewModel,
                    buttonInfoArray: [
                        ButtonInfo(view: .home,          icon: "house",      activation: true),
                        ButtonInfo(view: .conversation,  icon: "bubble",     activation: false),
                        ButtonInfo(view: .product,       icon: "tshirt",     activation: false),
                        ButtonInfo(view: .favourites,    icon: "star",       activation: false),
                        ButtonInfo(view: .outfit,        icon: "hanger",     activation: false),
                        ButtonInfo(view: .admin,         icon: "gear",       activation: false)
                    ]
                )
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(CustomColor.darkGray)
    }
}

#Preview {
    ContentView()
}
