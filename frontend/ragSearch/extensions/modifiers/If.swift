//
//  If.swift
//  app
//
//  Created by Lucas Grant on 2025-07-30.
//

import SwiftUI

extension View {
    @ViewBuilder func `if`<TrueContent: View, FalseContent: View>(
        _ condition: Bool,
        trueTransform: (Self) -> TrueContent,
        falseTransform: (Self) -> FalseContent
    ) -> some View {
        if condition {
            trueTransform(self)
        } else {
            falseTransform(self)
        }
    }

    @ViewBuilder func `if`<Content: View>(
        _ condition: Bool,
        transform: (Self) -> Content
    ) -> some View {
        if condition {
            transform(self)
        } else {
            self
        }
    }
}

