//
//  MenuSlider.swift
//  app
//
//  Created by Lucas Grant on 2025-07-28.
//

import SwiftUI

struct ButtonInfo: Identifiable {
    let id = UUID()
    let view: CurrentView
    let icon: String
    var activation: Bool
}

struct MenuSlider: View {
    @ObservedObject var viewModel: SharedViewModel
    @State var buttonInfoArray: [ButtonInfo]
    @Namespace private var namespace
    @State private var activeIndex: Int = 0
    
    var body: some View {
        ZStack(alignment: .bottom) {
            Color.clear
                .frame(maxHeight: .infinity)
//            ZStack {
//                Color.clear
//                    .frame(height: 40)
//                    .frame(maxWidth: .infinity)
                ZStack(alignment: .center) {
                    GeometryReader { geo in
                        if !buttonInfoArray.isEmpty {
                            Capsule()
                                .fill(CustomColor.lightGray)
                                .frame(width: (geo.size.width / CGFloat(buttonInfoArray.count))
//                                       * 0.9
                                       , height: geo.size.height)
                                .offset(x: geo.size.width / CGFloat(buttonInfoArray.count) * CGFloat(activeIndex)
//                                        * 1.025
                                )
                                .matchedGeometryEffect(id: "activeButton", in: namespace)
                        }
                    }
                    .allowsHitTesting(false)

                    HStack(spacing: 0) {
                        ForEach(buttonInfoArray.indices, id: \.self) { index in
                            Button(action: {
                                viewModel.currentView = buttonInfoArray[index].view
                                withAnimation(.spring(response: 0.4, dampingFraction: 0.9)) {
                                    activeIndex = index
                                }
                            }) {
                                Image(systemName: buttonInfoArray[index].icon)
                                    .font(.system(size: 16))
                                    .fontWeight(.bold)
                                    .foregroundColor(CustomColor.white)
                                    .frame(height: 40)
                                    .frame(maxWidth: .infinity)
                                    
                                    .clipShape(Capsule())
                            }
                        }
                    }
                }
                .frame(height: 40)
            .padding(.horizontal, 10)
            .padding(.vertical, 8)
            .background(CustomColor.gray)
            .clipShape(Capsule())
            .overlay(
                Capsule()
                    .stroke(CustomColor.lightGray, lineWidth: 2)
            )
            
        }
        .onAppear() {
            for index in buttonInfoArray.indices {
                if buttonInfoArray[index].view == viewModel.currentView {
                    buttonInfoArray[index].activation = true
                    activeIndex = index
                } else {
                    buttonInfoArray[index].activation =  false
                }
            }
        }
        .onChange(of: viewModel.currentView) { oldView, newView in

            for index in buttonInfoArray.indices {
                if buttonInfoArray[index].view == newView {
                    buttonInfoArray[index].activation = true
                    activeIndex = index
                } else {
                    buttonInfoArray[index].activation =  false
                }
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 36)
        .ignoresSafeArea()
    }
}

#Preview {
    ContentView(.menu)
}





//        .onChange(of: viewModel.currentView) { oldView, newView in
//            for index in buttonInfoArray.indices {
////                withAnimation(.spring(response: 0.4, dampingFraction: 0.9)) {
//                    buttonInfoArray[index].activation = (buttonInfoArray[index].view == newView)
////                }
//            }
//        }



//                HStack {
//
//                    ForEach(buttonInfoArray.indices, id: \.self) { index in
//                        Button(action: {
//                            viewModel.currentView = buttonInfoArray[index].view
//                            withAnimation(.spring(response: 0.4, dampingFraction: 0.9)) {
//                                activeIndex = index
//                            }
//                        }) {
//                            CapsuleButton(
//                                icon: buttonInfoArray[index].icon,
//                                outline: false,
//                                background: false
//                            )
//                        }
//                    }
//                }
//            }
