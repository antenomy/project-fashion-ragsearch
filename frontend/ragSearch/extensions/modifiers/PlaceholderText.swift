//
//  BasicText.swift
//  app
//
//  Created by Lucas Grant on 2025-07-26.
//
import SwiftUI

struct PlaceholderText: ViewModifier {
    let size: CGFloat
 
    func body(content: Content) -> some View {
        content
            .font(Font.custom("HM Sans", size: size))
            .foregroundColor(CustomColor.lightGray)
    }
}

extension View {
    func placeholderText(size: CGFloat) -> some View {
        self.modifier(PlaceholderText(size: size))
    }
}
