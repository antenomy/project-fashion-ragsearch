//
//  BasicText.swift
//  app
//
//  Created by Lucas Grant on 2025-07-26.
//
import SwiftUI

struct RoundedBox: ViewModifier {
    let cornerRadius: CGFloat
    let paddingOn: Bool
 
    func body(content: Content) -> some View {
        content
            .padding(paddingOn ? 16 : 0)
            .background(CustomColor.gray)
            .cornerRadius(cornerRadius)
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius)
                    .stroke(CustomColor.lightGray, lineWidth: 2)
            )
    }
}

extension View {
    func roundedBox(
        cornerRadius: CGFloat = 20,
        paddingOn: Bool = true
    ) -> some View {
        self.modifier(RoundedBox(
            cornerRadius: cornerRadius,
            paddingOn: paddingOn
        ))
    }
}
