//
//  BasicText.swift
//  app
//
//  Created by Lucas Grant on 2025-07-26.
//
import SwiftUI

struct BasicText: ViewModifier {
    let size: CGFloat
 
    func body(content: Content) -> some View {
        content
            .font(Font.custom("HM Sans", size: size))
            .foregroundColor(CustomColor.white)
    }
}

extension View {
    func basicText(size: CGFloat) -> some View {
        self.modifier(BasicText(size: size))
    }
}
