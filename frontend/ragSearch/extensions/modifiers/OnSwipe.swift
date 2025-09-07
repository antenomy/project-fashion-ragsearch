//
//  Untitled.swift
//  app
//
//  Created by Lucas Grant on 2025-07-26.
//
import SwiftUI

struct OnSwipe: ViewModifier {
    var up: () -> Void
    var down: () -> Void
    
//    init(
//        up: @escaping () -> Void = {},
//        down: @escaping () -> Void = {}
//        
//    ) {
//        self.up = up
//        self.down = down
//    }
    
    func body(content: Content) -> some View {
        content
            .gesture(
                DragGesture(minimumDistance: 20, coordinateSpace: .local)
                    .onEnded { value in
                        let verticalAmount = value.translation.height
                        
                        if verticalAmount < -20 {
                            // Swipe up
                            up()
                        } else if verticalAmount > 20 {
                            // Swipe down
                            down()
                        }
                    }
            )
    }
}

extension View {
    func onSwipe(
        up: @escaping () -> Void = {},
        down: @escaping () -> Void = {}
    ) -> some View {
        self.modifier(OnSwipe(
            up: up,
            down: down
        ))
    }
}
