//
//  CircleButton.swift
//  app
//
//  Created by Lucas Grant on 2025-07-26.
//

import SwiftUI

struct CircleButton: View {
    let iconPath: String
    let size: CGFloat
    let fontSize: CGFloat
    
    init (
        icon: String,
        size: Int = 40
    ) {
        self.iconPath = icon
        self.size = CGFloat(size)
        self.fontSize = CGFloat((size * 2) / 5)
    }
   
    var body: some View {
        Image(systemName: iconPath)
            .font(.system(size: fontSize))
            .fontWeight(.bold)
            .foregroundColor(CustomColor.white)
            .frame(width: CGFloat(size), height: CGFloat(size))
            .background(CustomColor.gray)
            .clipShape(Circle())
            .overlay(
                Circle()
                    .stroke(CustomColor.lightGray, lineWidth: 2)
            )
    }
}
