//
//  RoundedCornerShape.swift
//  ragSearch
//
//  Created by Lucas Grant on 2025-08-11.
//

import SwiftUI

struct RoundedCornerShape: Shape {
    var radius: CGFloat = 20
    var corners: UIRectCorner = [.topLeft, .topRight, .bottomLeft]

    func path(in rect: CGRect) -> Path {
        let path = UIBezierPath(
            roundedRect: rect,
            byRoundingCorners: corners,
            cornerRadii: CGSize(width: radius, height: radius)
        )
        return Path(path.cgPath)
    }
}
