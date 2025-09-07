//
//  AdminView.swift
//  app
//
//  Created by Lucas Grant on 2025-07-25.
//

import SwiftUI

struct OutfitView : View {
    @ObservedObject var viewModel: SharedViewModel
    
    init(_ viewModel: SharedViewModel) {
        self.viewModel = viewModel
    }
    
    var body: some View {
        Text("OUTFIT")
            .basicText(size: 24)

    }
}
