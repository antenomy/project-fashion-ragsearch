//
//  SharedViewModel.swift
//  app
//
//  Created by Lucas Grant on 2025-07-25.
//

import SwiftUI
import SwiftData

class SharedViewModel: ObservableObject {
    @Published var showMenuSlider = true
    @Published var currentView: CurrentView
    @Published var startView: CurrentView
   
    @Query var favourites: [Favourite]
    
    init(
        startView: CurrentView
    ) {
        self.currentView = startView
        self.startView = startView
    }
}
