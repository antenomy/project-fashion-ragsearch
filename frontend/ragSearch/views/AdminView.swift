//
//  AdminView.swift
//  app
//
//  Created by Lucas Grant on 2025-07-25.
//

import SwiftUI

struct AdminView : View {
    @ObservedObject var viewModel: SharedViewModel
    
    init(_ viewModel: SharedViewModel) {
        self.viewModel = viewModel
    }
    
    
    var body: some View {
        Text("ADMIN")
            .basicText(size: 24)
    }
}
