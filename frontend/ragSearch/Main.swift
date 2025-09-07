//
//  ragSearchApp.swift
//  ragSearch
//
//  Created by Lucas Grant on 2025-08-01.
//

import SwiftUI
import SwiftData

@main
struct Main: App {

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Favourite.self)
    }
}
